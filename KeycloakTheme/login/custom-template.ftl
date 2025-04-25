<#macro baseLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>РЖД</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
              integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

        <link rel="stylesheet" href="${url.resourcesPath}/css/index.css">
        <link rel="icon" type="image/x-icon" href="${url.resourcesPath}/img/favicon.svg">
    </head>
    <body class="${bodyClass}">

    <div class="container d-flex align-items-center justify-content-center min-vh-100">
        <div class="w-100" style="max-width: 400px;">
            <!-- Logo -->
            <div class="text-center mb-4">
                <img src="${url.resourcesPath}/img/favicon.svg" alt="Logo" class="img-fluid rounded p-2" style="background-color: #e21a1a; max-width: 100px;">
            </div>

            <!-- Card -->
            <div class="card shadow">
                <div class="card-body">
                    <#nested "form">
                </div>
            </div>
        </div>
    </div>

    </body>
    </html>
</#macro>
