from crispy_forms.helper import FormHelper


class HorizontalFormMixin:
    @property
    def helper(self):
        helper = FormHelper(self)

        helper.form_tag = False
        helper.disable_csrf = True
        helper.form_class = "horizontal-form needs-validation form-horizontal"

        helper.label_class = "col-md-4 col-lg-3 col-form-label"
        helper.field_class = "col-md-8 col-lg-9 form-field"

        helper.error_text_inline = True
        helper.help_text_inline = True
        helper.form_show_labels = True
        return helper


class CheckFormMixin:
    @property
    def helper(self):
        helper = FormHelper(self)

        helper.form_tag = False
        helper.disable_csrf = True

        helper.error_text_inline = True
        helper.help_text_inline = True
        helper.form_show_labels = True
        return helper
