<#import "custom-template.ftl" as layout>
<#import "fields.ftl" as field>


<@layout.baseLayout displayMessage=messagesPerField.exists('global') displayRequiredFields=true; section>
    <h4 class="card-title text-center mb-4">${msg("registerTitle")}</h4>

    <form
            id="kc-register-form"
            action="${url.registrationAction}"
            method="post"
            novalidate="novalidate"
    >
        <#list profile.attributes as attribute>
            <@field.input name="${attribute.name}" label=advancedMsg(attribute.displayName!'') error=kcSanitize(messagesPerField.get('${attribute.name}'))?no_esc required=true value=attribute.value!'' />
        </#list>

        <@field.password name="password" required=true label=msg("password") autocomplete="new-password" />

        <@field.password name="password-confirm" required=true label=msg("passwordConfirm") autocomplete="new-password" />

        <button type="submit" class="btn btn-primary w-100 mb-3">${msg("doRegister")}</button>

        <div class="register-link text-center">
            <a href="${url.loginUrl}" class="text-decoration-none">${kcSanitize(msg("backToLogin"))?no_esc}</a>
        </div>
    </form>

</@layout.baseLayout>
