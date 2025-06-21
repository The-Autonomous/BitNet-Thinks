@echo off
setlocal EnableDelayedExpansion

rem ── Find all cmake.exe and pick the highest version ──────────────────────
set best_num=0
set best_cmake=

for /f "delims=" %%x in ('where cmake 2^>nul') do (
    rem get the version string, e.g. "cmake version 3.24.1"
    for /f "tokens=3" %%v in ('"%%x" --version') do (
        set ver=%%v
    )
    echo Found CMake at %%x version !ver!

    rem convert ver X.Y.Z to integer for comparison: X*10000 + Y*100 + Z
    for /f "tokens=1-3 delims=." %%a in ("!ver!") do (
        set /a vernum=(%%a*10000)+(%%b*100)+(%%c)
    )
    if !vernum! gtr !best_num! (
        set best_num=!vernum!
        set best_cmake=%%x
    )
)

if not defined best_cmake (
    echo ERROR: No cmake.exe found in PATH.
    exit /b 1
)

echo.
echo Using CMake: "%best_cmake%" (numeric id: !best_num!)
echo.

rem ── Prepare build directory ──────────────────────────────────────────────
set BUILD_DIR=build
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"
pushd "%BUILD_DIR%"

rem ── Run CMake configure + Ninja build ────────────────────────────────────
"%best_cmake%" -G Ninja ..  || (
    echo CMake configuration failed!
    popd
    exit /b 1
)

ninja || (
    echo Ninja build failed!
    popd
    exit /b 1
)

echo.
echo Build complete!
popd
endlocal
