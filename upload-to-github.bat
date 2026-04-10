@echo off
chcp 65001 >nul
echo ========================================
echo   DXF to KML Converter - GitHub Upload
echo ========================================
echo.
echo GitHub Username: wangningping
echo Repository: dxf2kml
echo.
echo [1/3] Initializing Git repository...
echo.

REM Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git not found. Please install Git first.
    echo Download: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize Git repository
if not exist .git (
    echo Initializing Git repository...
    git init
) else (
    echo Git repository already exists
)

echo.
echo [2/3] Adding all files to Git...
echo.
git add .

echo.
echo [3/3] Committing changes...
echo.
git commit -m "Initial commit: DXF to KML Converter with CGCS2000 support v1.0.0"

echo.
echo ========================================
echo   Step 1 Complete!
echo ========================================
echo.
echo Next steps (please follow carefully):
echo.
echo 1. Create repository on GitHub:
echo    Visit: https://github.com/new
echo    Repository name: dxf2kml
echo    Description: Convert DXF files to KML format with CGCS2000 support
echo    Visibility: Public
echo    [ ] DO NOT check "Add a README file"
echo    [ ] DO NOT check "Add .gitignore"
echo    [ ] DO NOT check "Add license"
echo    Click "Create repository"
echo.
echo 2. After creating the repository, push your code:
echo.
echo    cd C:\Users\wnp\.copaw\workspaces\default\dwg2kml
echo    git remote add origin https://github.com/wangningping/dxf2kml.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Or using SSH (if you configured SSH keys):
echo    git remote add origin git@github.com:wangningping/dxf2kml.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
echo.
echo After pushing, visit:
echo https://github.com/wangningping/dxf2kml
echo.
echo Press any key to continue...
pause >nul
