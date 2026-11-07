const API_BASE_URL = "http://127.0.0.1:8000";

const fileList = document.getElementById("fileList");
const totalFiles = document.getElementById("totalFiles");
const totalLines = document.getElementById("totalLines");
const projectStatus = document.getElementById("projectStatus");
const projectStatusText = document.getElementById("projectStatusText");

const connectionDot = document.getElementById("connectionDot");
const connectionText = document.getElementById("connectionText");

const analysisForm = document.getElementById("analysisForm");
const userRequest = document.getElementById("userRequest");
const analyzeButton = document.getElementById("analyzeButton");
const buttonText = document.getElementById("buttonText");

const resultContent = document.getElementById("resultContent");
const copyButton = document.getElementById("copyButton");
const refreshButton = document.getElementById("refreshButton");

const modeTitle = document.getElementById("modeTitle");
const modeDescription = document.getElementById("modeDescription");
const projectSelect = document.getElementById("projectSelect");

let currentMode = "project_qa";
let currentProjectId = "";
let latestResult = "";


const modes = {
    project_qa: {
        title: "Ask about your project",
        description: "Ask questions about your source code.",
        suggestions: [
            "Explain this project",
            "What does main.py do?",
            "What is the purpose of database.py?"
        ]
    },

    architecture: {
        title: "Architecture analysis",
        description: "Understand modules and how they connect.",
        suggestions: [
            "Explain the project architecture",
            "How are the modules connected?",
            "Explain the application flow"
        ]
    },

    code_review: {
        title: "Code review",
        description: "Identify potential bugs and code issues.",
        suggestions: [
            "Review all the code",
            "Find bugs in this project",
            "Check error handling"
        ]
    },

    structure_review: {
        title: "Structure review",
        description: "Evaluate the project folder organization.",
        suggestions: [
            "Review the folder structure",
            "How can I improve this structure?",
            "Suggest better file organization"
        ]
    },

    project_report: {
        title: "Project report",
        description: "Generate an overall project assessment.",
        suggestions: [
            "Generate a project report",
            "Give an overall project summary",
            "What improvements should I make?"
        ]
    }
};


// Escape dynamic values before inserting them into HTML.
function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, function (character) {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        };

        return entities[character];
    });
}


// Check backend connection.
async function checkBackend() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        connectionDot.style.background = "var(--green)";
        connectionText.textContent = "Backend connected";

        return true;

    } catch (error) {
        connectionDot.style.background = "var(--red)";
        connectionText.textContent = "Backend disconnected";

        projectStatus.textContent = "Offline";
        projectStatusText.textContent = "Start your FastAPI server";

        return false;
    }
}


// Fetch approved projects and populate dropdown.
async function loadProjects() {
    const response = await fetch(`${API_BASE_URL}/projects`);

    if (!response.ok) {
        throw new Error("Could not retrieve approved projects.");
    }

    const data = await response.json();
    const projects = data.projects || [];

    projectSelect.innerHTML = "";

    const availableProjects = projects.filter(
        project => project.available
    );

    if (availableProjects.length === 0) {
        projectSelect.innerHTML =
            `<option value="">No available projects</option>`;

        throw new Error("No approved project folders are available.");
    }

    availableProjects.forEach(function (project) {
        const option = document.createElement("option");

        option.value = project.project_id;
        option.textContent = project.name;

        projectSelect.appendChild(option);
    });

    // Select the default project when available.
    const defaultProject = availableProjects.find(
        project => project.project_id === "sample_project"
    );

    currentProjectId = defaultProject
        ? defaultProject.project_id
        : availableProjects[0].project_id;

    projectSelect.value = currentProjectId;
    document.getElementById("workspaceName").textContent =
    projectSelect.options[projectSelect.selectedIndex].textContent;     
    await loadProject(currentProjectId);
}


// Add a new project using the backend folder picker.
const addProjectButton = document.getElementById("addProjectButton");
const addProjectStatus = document.getElementById("addProjectStatus");

addProjectButton.addEventListener("click", async function () {

    addProjectButton.disabled = true;
    addProjectButton.textContent = "Opening folder picker...";

    addProjectStatus.textContent =
        "Choose a project folder on your computer.";

    try {

        const response = await fetch(
            `${API_BASE_URL}/projects/add`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Could not add project."
            );
        }

        if (data.cancelled) {
            addProjectStatus.textContent =
                "Project selection cancelled.";

            return;
        }

        addProjectStatus.textContent =
            `${data.project.name} added successfully.`;

        // Reload dropdown and scan the newly added project.
        await loadProjects();

        // Select the newly registered project.
        currentProjectId = data.project.project_id;
        projectSelect.value = currentProjectId;

        await loadProject(currentProjectId);

        const workspaceName =
            document.getElementById("workspaceName");

        if (workspaceName) {
            workspaceName.textContent = data.project.name;
        }

    } catch (error) {

        addProjectStatus.textContent = error.message;

    } finally {

        addProjectButton.disabled = false;

        addProjectButton.innerHTML =
            "<span>＋</span> Add Project";

    }

});



// Scan and display the selected project.
async function loadProject(projectId) {
    fileList.innerHTML = `
        <div class="empty-state">Scanning selected project...</div>
    `;

    projectStatus.textContent = "Scanning";
    projectStatusText.textContent = "Please wait";

    try {
        const response = await fetch(
            `${API_BASE_URL}/scan-project?project_id=${encodeURIComponent(projectId)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Project scanning failed.");
        }

        const files = data.files || [];

        totalFiles.textContent = data.total_files ?? files.length;
        totalLines.textContent = "--";

        projectStatus.textContent = "Ready";
        projectStatusText.textContent =
            `${data.project_name} scanned successfully`;

        if (files.length === 0) {
            fileList.innerHTML = `
                <div class="empty-state">
                    No supported files found in this project.
                </div>
            `;
        } else {
            fileList.innerHTML = files.map(function (file) {
                const filename = file.split(/[\\/]/).pop();

                const extension = filename.includes(".")
                    ? filename.split(".").pop().toUpperCase()
                    : "FILE";

                return `
                    <div class="file-item">
                        <span class="file-symbol">📄</span>

                        <div class="file-details">
                            <strong>${escapeHTML(file)}</strong>
                            <small>Project source file</small>
                        </div>

                        <span class="file-type">
                            ${escapeHTML(extension)}
                        </span>
                    </div>
                `;
            }).join("");
        }

        const skippedFiles = data.skipped_files || [];
        const skippedContainer =
            document.getElementById("skippedFiles");

        skippedContainer.textContent = skippedFiles.length > 0
            ? `${skippedFiles.length} file(s) skipped during scanning.`
            : "";

        return data;

    } catch (error) {
        fileList.innerHTML = `
            <div class="empty-state">
                Unable to load project files.<br>
                ${escapeHTML(error.message)}
            </div>
        `;

        projectStatus.textContent = "Error";
        projectStatusText.textContent = "Project scan failed";

        throw error;
    }
}


// Change selected project.
projectSelect.addEventListener("change", async function () {
    const selectedProjectId = projectSelect.value;

    if (!selectedProjectId) {
        return;
    }

    currentProjectId = selectedProjectId;
    document.getElementById("workspaceName").textContent =
    projectSelect.options[projectSelect.selectedIndex].textContent;
    totalLines.textContent = "--";

    // Clear previous analysis when changing projects.
    latestResult = "";
    copyButton.disabled = true;

    resultContent.innerHTML = `
        <div class="result-placeholder">
            <div class="placeholder-icon">✦</div>
            <h3>Project changed</h3>
            <p>Ask a question to analyze the newly selected project.</p>
        </div>
    `;

    try {
        await loadProject(currentProjectId);
    } catch (error) {
        console.error(error);
    }
});


// Change analysis mode.
function selectMode(mode) {
    if (!modes[mode]) {
        return;
    }

    currentMode = mode;

    const selectedMode = modes[mode];

    document.querySelectorAll(".nav-item").forEach(function (item) {
        item.classList.toggle(
            "active",
            item.dataset.mode === mode
        );
    });

    modeTitle.textContent = selectedMode.title;
    modeDescription.textContent = selectedMode.description;

    const suggestionsContainer =
        document.getElementById("suggestions");

    suggestionsContainer.innerHTML =
        selectedMode.suggestions.map(function (suggestion) {
            return `
                <button
                    type="button"
                    class="suggestion-chip"
                    data-suggestion="${escapeHTML(suggestion)}"
                >
                    ${escapeHTML(suggestion)}
                </button>
            `;
        }).join("");
}


// Suggestion buttons.
document.getElementById("suggestions").addEventListener(
    "click",
    function (event) {
        const button = event.target.closest(".suggestion-chip");

        if (!button) {
            return;
        }

        userRequest.value = button.dataset.suggestion;
        userRequest.focus();
    }
);


// Navigation buttons.
document.querySelectorAll(".nav-item").forEach(function (button) {
    button.addEventListener("click", function () {
        selectMode(button.dataset.mode);
    });
});


// Display loading state.
function showLoading() {
    resultContent.innerHTML = `
        <div class="loading-state">
            <div class="loading-spinner"></div>

            <h3>Analyzing your project...</h3>

            <p>
                CodePilot is scanning your selected project
                and generating an answer.
            </p>
        </div>
    `;
}


// Display AI result.
function displayResult(response) {
    latestResult = response;

    if (
        typeof marked === "undefined" ||
        typeof DOMPurify === "undefined"
    ) {
        resultContent.textContent = response;
    } else {
        const html = marked.parse(response);
        resultContent.innerHTML = DOMPurify.sanitize(html);

        if (typeof hljs !== "undefined") {
            resultContent.querySelectorAll("pre code").forEach(
                function (block) {
                    hljs.highlightElement(block);
                }
            );
        }
    }

    copyButton.disabled = false;
}


// Analyze selected project.
analysisForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const request = userRequest.value.trim();

    if (!request) {
        return;
    }

    if (!currentProjectId) {
        alert("Please select a project first.");
        return;
    }

    analyzeButton.disabled = true;
    buttonText.textContent = "Analyzing...";
    copyButton.disabled = true;

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_request: request,
                project_id: currentProjectId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "The analysis request failed."
            );
        }

        displayResult(data.response);

        if (data.project_summary) {
            totalFiles.textContent =
                data.project_summary.total_files ?? "--";

            totalLines.textContent =
                data.project_summary.total_lines ?? "--";
        }

    } catch (error) {
        latestResult = "";

        resultContent.innerHTML = `
            <div class="error-message">
                <strong>Analysis failed</strong>
                <p>${escapeHTML(error.message)}</p>
                <p>
                    Check the backend terminal for details.
                </p>
            </div>
        `;

        copyButton.disabled = true;

    } finally {
        analyzeButton.disabled = false;
        buttonText.textContent = "Analyze project";
    }
});


// Copy result.
copyButton.addEventListener("click", async function () {
    if (!latestResult) {
        return;
    }

    try {
        await navigator.clipboard.writeText(latestResult);

        copyButton.textContent = "Copied!";

        setTimeout(function () {
            copyButton.textContent = "Copy result";
        }, 1500);

    } catch (error) {
        copyButton.textContent = "Copy failed";
    }
});


// Refresh selected project.
refreshButton.addEventListener("click", async function () {
    if (!currentProjectId) {
        return;
    }

    refreshButton.disabled = true;
    refreshButton.textContent = "Refreshing...";

    try {
        await loadProject(currentProjectId);
    } catch (error) {
        console.error(error);
    } finally {
        refreshButton.disabled = false;
        refreshButton.textContent = "↻ Refresh project";
    }
});


// Theme toggle.
const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("light-theme");

    const isLight =
        document.body.classList.contains("light-theme");

    themeToggle.textContent = isLight ? "☾" : "☼";
});


// Start application.
async function initializeApp() {
    const connected = await checkBackend();

    if (connected) {
        try {
            await loadProjects();
        } catch (error) {
            console.error(error);

            fileList.innerHTML = `
                <div class="empty-state">
                    ${escapeHTML(error.message)}
                </div>
            `;
        }
    }

    selectMode("project_qa");
}

initializeApp();