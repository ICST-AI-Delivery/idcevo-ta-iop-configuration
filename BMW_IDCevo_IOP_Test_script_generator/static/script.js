async function uploadXML(){
let file =
document.getElementById("xmlFile").files[0]
let formData=new FormData()
formData.append("file",file)
let res=await fetch(
"/upload_xml",
{
method:"POST",
body:formData
}
)
let tests=await res.json()
let div=document.getElementById("testList")
div.innerHTML=""
tests.forEach(t=>{
div.innerHTML+=
`
<input type="checkbox" value="${t.id}">
${t.id} — ${t.name}
<br>
`
})
}

async function importTests(){
let selected=[]
document
.querySelectorAll(
"#testList input:checked"
)
.forEach(cb=>selected.push(cb.value))
await fetch(
"/import_tests",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({selected})
}
)
loadTable()
}

let csvData = []

async function loadTable(){
let res=
await fetch("/get_csv")
let data=
await res.json()
csvData = data // Store data globally for editing
let table=
document.getElementById("table")
table.innerHTML=""
data.forEach((row, index) => {
table.innerHTML+=`
<tr>
<td>
${row["Test Case ID"] || ""}
</td>
<td>
${row["Test Name"]}
</td>
<td class="editable-cell" contenteditable="true" data-row="${index}" data-field="Test Case Precondition">
${row["Test Case Precondition"]}
</td>
<td class="editable-cell" contenteditable="true" data-row="${index}" data-field="Test Case Description">
${row["Test Case Description"]}
</td>
<td class="editable-cell" contenteditable="true" data-row="${index}" data-field="Test Case Expected Result">
${row["Test Case Expected Result"]}
</td>
<td class="editable-cell" contenteditable="true" data-row="${index}" data-field="Test Script Description">
${row["Test Script Description"]}
</td>
</tr>
`
})

// Add event listeners for editable cells
setTimeout(() => {
    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('input', function() {
            const row = parseInt(this.getAttribute('data-row'))
            const field = this.getAttribute('data-field')
            csvData[row][field] = this.textContent
            showSaveButton()
        })
    })
    
    // Add click-to-expand functionality for Test Script Description column
    addTestScriptDescriptionExpandHandlers()
}, 100)
}

async function generateDescriptions(){
console.log("DEBUG: generateDescriptions() function called!")

try {
console.log("DEBUG: Starting API call to /generate_descriptions")
// Show progress container
showProgressBar("Analyzing existing patterns and generating descriptions...", 0)

const response = await fetch("/generate_descriptions", {method:"POST"})
console.log("DEBUG: Received response from server:", response)

const result = await response.json()
console.log("DEBUG: Parsed JSON result:", result)

if (result.success) {
console.log("DEBUG: Result was successful")
// Update progress to completion
updateProgressBar("✅ Generation Complete!", 100)

if (result.updated_count > 0) {
showStatusMessage(`✅ Successfully generated descriptions for ${result.updated_count} test cases!`, true)
// Auto-reload table to show the updates
loadTable()
} else {
showStatusMessage(`ℹ️ ${result.message}`, true)
}

// Hide progress bar after 2 seconds
setTimeout(() => {
hideProgressBar()
}, 2000)

} else {
console.log("DEBUG: Result was not successful:", result.message)
hideProgressBar()
showStatusMessage(`❌ Error: ${result.message}`, false)
}
} catch (error) {
console.error("DEBUG: Caught error:", error)
hideProgressBar()
showStatusMessage("❌ Error communicating with server", false)
}
}

function showProgressBar(text, progress) {
const container = document.getElementById('progressContainer')
const progressText = document.getElementById('progressText')
const progressBar = document.getElementById('progressBar')

container.style.display = 'block'
progressText.textContent = text
progressBar.style.width = progress + '%'
}

function updateProgressBar(text, progress) {
const progressText = document.getElementById('progressText')
const progressBar = document.getElementById('progressBar')

progressText.textContent = text
progressBar.style.width = progress + '%'
}

function hideProgressBar() {
const container = document.getElementById('progressContainer')
container.style.display = 'none'
}

async function generateScripts(){
console.log("DEBUG: generateScripts() function called!")

try {
    console.log("DEBUG: Starting API call to /generate_scripts")
    // Show progress container
    showProgressBar("Starting script generation...", 0)

    // Start the generation process (don't wait for completion)
    fetch("/generate_scripts", {method:"POST"})
        .then(response => response.json())
        .then(result => {
            console.log("DEBUG: Generation process completed:", result)
            if (!result.success) {
                hideProgressBar()
                showStatusMessage(`❌ Error: ${result.message}`, false)
            }
        })
        .catch(error => {
            console.error("DEBUG: Generation process error:", error)
            hideProgressBar()
            showStatusMessage("❌ Error during script generation", false)
        })

    // Start polling for progress updates
    const progressInterval = setInterval(async () => {
        try {
            const progressResponse = await fetch("/get_script_progress", {method:"GET"})
            const progress = await progressResponse.json()
            
            console.log("DEBUG: Progress update:", progress)
            
            if (progress.status === 'processing') {
                // Cap progress at 95% during processing phase
                const percentage = progress.total > 0 ? Math.min(95, Math.round((progress.current / progress.total) * 95)) : 0
                updateProgressBar(progress.message, percentage)
            } else if (progress.status === 'completed') {
                // Clear the polling interval
                clearInterval(progressInterval)
                
                // Only now show 100% completion
                updateProgressBar("✅ Script Generation Complete!", 100)
                
                if (progress.completed_scripts && progress.completed_scripts.length > 0) {
                    showStatusMessage(`✅ Successfully generated ${progress.completed_scripts.length} Python scripts! Scripts saved to: D:/traget/IDCevo/BMW IDCevo IOP demo/scripts`, true)
                } else {
                    showStatusMessage(`ℹ️ ${progress.message}`, true)
                }
                
                // Hide progress bar after 3 seconds
                setTimeout(() => {
                    hideProgressBar()
                }, 3000)
                
            } else if (progress.status === 'error') {
                // Clear the polling interval
                clearInterval(progressInterval)
                
                hideProgressBar()
                showStatusMessage(`❌ Error: ${progress.message}`, false)
            }
        } catch (error) {
            console.error("DEBUG: Error polling progress:", error)
            // Continue polling - don't break on temporary errors
        }
    }, 1000) // Poll every second
    
    // Safety timeout to stop polling after 5 minutes
    setTimeout(() => {
        clearInterval(progressInterval)
        console.log("DEBUG: Progress polling timeout reached")
    }, 300000) // 5 minutes

} catch (error) {
    console.error("DEBUG: Caught error:", error)
    hideProgressBar()
    showStatusMessage("❌ Error communicating with server", false)
}
}

function showSaveButton() {
    document.getElementById('saveButton').style.display = 'block'
}

function hideSaveButton() {
    document.getElementById('saveButton').style.display = 'none'
}

function showStatusMessage(message, isSuccess = true) {
    const statusDiv = document.getElementById('statusMessage')
    statusDiv.textContent = message
    statusDiv.className = `status-message ${isSuccess ? 'status-success' : 'status-error'}`
    statusDiv.style.display = 'block'
    
    setTimeout(() => {
        statusDiv.style.display = 'none'
    }, 3000)
}

async function saveCSV() {
    try {
        const saveButton = document.getElementById('saveButton')
        saveButton.disabled = true
        saveButton.textContent = 'Saving...'
        
        const response = await fetch('/save_csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: csvData })
        })
        
        const result = await response.json()
        
        if (result.success) {
            showStatusMessage('✅ Changes saved successfully!')
            hideSaveButton()
        } else {
            showStatusMessage(`❌ Error saving: ${result.message}`, false)
        }
    } catch (error) {
        console.error('Error:', error)
        showStatusMessage('❌ Error communicating with server', false)
    } finally {
        const saveButton = document.getElementById('saveButton')
        saveButton.disabled = false
        saveButton.textContent = 'Save Changes'
    }
}

function addTestScriptDescriptionExpandHandlers() {
    // Add click handlers for Test Script Description cells (6th column)
    document.querySelectorAll('td:nth-child(6)').forEach(cell => {
        // Skip if this cell doesn't have content
        if (!cell.textContent.trim()) return;
        
        cell.addEventListener('click', function(e) {
            // Prevent event from bubbling to document
            e.stopPropagation();
            
            // Collapse all other expanded cells first
            document.querySelectorAll('td:nth-child(6).expanded').forEach(otherCell => {
                if (otherCell !== this) {
                    otherCell.classList.remove('expanded');
                }
            });
            
            // Toggle this cell
            this.classList.toggle('expanded');
        });
    });
    
    // Add document click handler to collapse expanded cells when clicking elsewhere
    document.addEventListener('click', function(e) {
        // Check if the click was outside any Test Script Description cell
        if (!e.target.closest('td:nth-child(6)')) {
            document.querySelectorAll('td:nth-child(6).expanded').forEach(cell => {
                cell.classList.remove('expanded');
            });
        }
    });
}

loadTable()
