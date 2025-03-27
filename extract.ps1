$directory = "C:\git\ThinkingInTypes_Examples"

mdvalid -d .\Chapters\
Write-Host "WARNING: You are about to delete the examples in: $directory"
$response = Read-Host "Are you sure? Type 'y' to continue"

if ($response -eq 'y') {
    # Remove the directory
    if (Test-Path $directory) {
        repoclean -a $directory
    }
    else {
        Write-Host "Directory does not exist: $directory"
    }

    # Run mdextract
    mdextract -d Chapters C:\git\ThinkingInTypes_Examples
}
else {
    Write-Host "Operation canceled."
}
