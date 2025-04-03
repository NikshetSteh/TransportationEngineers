<#macro baseLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>РЖД</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <link rel="stylesheet" href="${url.resourcesPath}/css/index.css">

    <link rel="icon" type="image/x-icon" href="${url.resourcesPath}/img/favicon.svg">
</head>
<body>

<div class="sign-in-container">
    <!-- Company Logo -->
    <div class="company-logo">
        <img src="${url.resourcesPath}/img/favicon.svg" alt="Company Logo" class="img-fluid p-3 rounded" style="background: #e21a1a">
    </div>

    <!-- Sign-In Card -->
    <div class="card">
        <div class="card-body">
            <#nested "form">
        </div>
    </div>
</div>
</body>
</html>
</#macro>