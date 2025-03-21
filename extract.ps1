$directory = "C:\git\ThinkingInTypes_Examples\src"

mdvalid -d .\Chapters\
Write-Host "WARNING: You are about to delete the directory: $directory"
$response = Read-Host "Are you sure? Type 'y' to continue"

if ($response -eq 'y') {
    # Remove the directory
    if (Test-Path $directory) {
        Remove-Item -Path $directory -Recurse -Force
        Write-Host "Deleted $directory"
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
