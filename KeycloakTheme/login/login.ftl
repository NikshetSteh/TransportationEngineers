<#import "custom-template.ftl" as layout>
<#import "fields.ftl" as field>

<@layout.baseLayout displayMessage=!messagesPerField.existsError('username','password') displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>

    <h4 class="card-title text-center mb-4">${msg("loginAccountTitle")}</h4>

    <form id="kc-form-login" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post" novalidate>

        <#assign label>
            <#if !realm.loginWithEmailAllowed>
                ${msg("username")}
            <#elseif !realm.registrationEmailAsUsername>
                ${msg("usernameOrEmail")}
            <#else>
                ${msg("email")}
            </#if>
        </#assign>

        <@field.input name="username" label=label error=kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc autofocus=true autocomplete="username" value=login.username!'' />

        <@field.password name="password" label=msg("password") error="" forgotPassword=realm.resetPasswordAllowed autofocus=usernameHidden?? autocomplete="current-password">
            <#if realm.rememberMe && !usernameHidden??>
                <@field.checkbox name="rememberMe" label=msg("rememberMe") value=login.rememberMe?? />
            </#if>
        </@field.password>

        <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="rememberMe" name="rememberMe"
                       <#if login.rememberMe??>checked</#if> />
                <label class="form-check-label" for="rememberMe">
                    ${msg("rememberMe")}
                </label>
            </div>

            <a href="${url.loginResetCredentialsUrl}" class="text-decoration-none">
                ${msg("doForgotPassword")}
            </a>
        </div>

        <button type="submit" class="btn btn-primary w-100 mb-3">${msg("doLogIn")}</button>

        <div class="text-center">
            ${msg("noAccount")} <a href="${url.registrationUrl}" class="text-decoration-none">${msg("doRegister")}</a>
        </div>

    </form>

</@layout.baseLayout>
