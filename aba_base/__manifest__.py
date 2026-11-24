{
    "name": "ABA Web Agency – Base setup",
    "version": "19.0.1.0.0",
    "summary": "Company, users and roles, Discuss channels, CRM team, booking page and settings for ABA Web Agency",
    "description": """
Rebuilds the ABA Web Agency setup done in the UI during Phase 0/1 (Nov 2026):
company identity + Italian e-invoicing data, document layout, 21 users with their
access level, Discuss channels, the CRM sales team with the leads@ alias, the
"Call Conoscitiva" booking page, 2FA / sign-up policy and Google sign-in.

Secrets (Google client secret, passwords, API keys) are NOT in this module.
See README.md before installing it on a database that already has this setup.
""",
    "author": "EEY AAY",
    "category": "Hidden",
    "license": "OEEL-1",
    "depends": [
        # Accounting + Italian localization
        "account_accountant",
        "l10n_it_edi",
        # Apps
        "contacts",
        "crm",
        "sale_management",
        "sale_timesheet",
        "project",
        "project_todo",
        "timesheet_grid",
        "hr",
        "hr_holidays",
        "calendar",
        "google_calendar",
        "appointment",
        "appointment_crm",
        "appointment_sms",
        "whatsapp",
        "spreadsheet_dashboard",
        # Security / login
        "auth_oauth",
        "auth_signup",
        "auth_totp_mail",
        # Gmail plugin
        "mail_plugin",
        "crm_mail_plugin",
        "project_mail_plugin",
    ],
    "data": [
        "data/res_lang_data.xml",
        "data/res_company_data.xml",
        "data/mail_data.xml",
        "data/settings_data.xml",
        "data/res_users_data.xml",
        "data/crm_team_data.xml",
        "data/discuss_channel_data.xml",
        "data/appointment_data.xml",
        "data/ir_filters_data.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
