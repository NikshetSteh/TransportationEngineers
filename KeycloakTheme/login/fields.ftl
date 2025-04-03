<#macro group name label error="" required=false>
    <div class="mb-3" xmlns="http://www.w3.org/1999/html">
        <label for="${name}" class="form-label">
            ${label}
        </label>

        <#nested>

        <div id="input-error-container-${name}">
            <#if error?has_content>
                <div aria-live="polite">
                    <div>
                        <div id="input-error-${name}">
                        <span>
                            ${error}
                        </span>
                        </div>
                    </div>
                </div>
            </#if>
        </div>
    </div>
</#macro>

<#macro errorIcon error="">
    <#if error?has_content>
        <span>
        <span>
          <i aria-hidden="true"></i>
        </span>
    </span>
    </#if>
</#macro>

<#macro input name label value="" required=false autocomplete="off" fieldName=name error=kcSanitize(messagesPerField.get(fieldName))?no_esc autofocus=false>
    <@group name=name label=label error=error required=required>
        <span>
        <input id="${name}" name="${name}" value="${value}" type="text" autocomplete="${autocomplete}"
               class="form-control"
               <#if autofocus>autofocus</#if>
                aria-invalid="<#if error?has_content>true</#if>"/>
        <@errorIcon error=error/>
    </span>
    </@group>
</#macro>

<#macro password name label value="" required=false forgotPassword=false fieldName=name error=kcSanitize(messagesPerField.get(fieldName))?no_esc autocomplete="off" autofocus=false>
    <@group name=name label=label error=error required=required>
        <div>
            <div>
                <!-- Add position: relative to the wrapper -->
                <span style="position: relative;">
            <!-- Password Input Field -->
            <input
                    id="${name}"
                    name="${name}"
                    value="${value}"
                    type="password"
                    autocomplete="${autocomplete}"
                    <#if autofocus>autofocus</#if>
                aria-invalid="<#if error?has_content>true</#if>"
                    class="form-control"
                    style="padding-right: 30px;"
            />
                    <!-- Toggle Button -->
            <button
                    type="button"
                    class="password-toggle-btn"
                    aria-label="Toggle password visibility"
                    onclick="togglePasswordVisibility('${name}')"
            >
                <img src="${url.resourcesPath}/img/visibility-off.svg"
                     alt="Toggle password visibility"
                     style="color: var(--bs-body-color)"
                     id="${name}-icon"
                >
            </button>
            <@errorIcon error=error/>
        </span>
            </div>
        </div>

        <!-- JavaScript for Toggle Functionality -->
        <script>
            function togglePasswordVisibility(inputId) {
                const inputField = document.getElementById(inputId);
                const icon = document.getElementById(inputId + `-icon`);

                if (inputField.type === 'password') {
                    // Change input type to text to show the password
                    inputField.type = 'text';
                    // Update the icon to "hide password" (SVG Eye-Off Icon)
                    icon.src = "${url.resourcesPath}/img/visibility.svg";
                } else {
                    // Change input type back to password to hide it
                    inputField.type = 'password';
                    // Update the icon to "show password" (SVG Eye Icon)
                    icon.src = "${url.resourcesPath}/img/visibility-off.svg";
                }
            }
        </script>
    </@group>
</#macro>
