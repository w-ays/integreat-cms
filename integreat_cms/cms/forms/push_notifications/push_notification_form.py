import datetime
import zoneinfo

from django import forms
from django.conf import settings
from django.forms import CheckboxSelectMultiple
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...models import PushNotification
from ..custom_model_form import CustomModelForm


class PushNotificationForm(CustomModelForm):
    """
    Form for creating and modifying push notification objects
    """

    schedule_send = forms.BooleanField(label=_("Schedule sending"), required=False)
    scheduled_send_date_day = forms.DateField(
        label=_("Scheduled send day"),
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    scheduled_send_date_time = forms.TimeField(
        label=_("Scheduled send time"),
        required=False,
        widget=forms.TimeInput(
            format="%H:%M",
            attrs={
                "type": "time",
                "step": str(settings.FCM_SCHEDULE_INTERVAL_MINUTES * 60),
            },
        ),
    )

    def __init__(
        self,
        regions=None,
        selected_regions=None,
        disabled=False,
        template=False,
        **kwargs,
    ):
        r"""
        Initialize push notification form

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict
        """
        # Instantiate CustomModelForm
        super().__init__(**kwargs)

        # Make fields disabled when push notification was already sent
        if self.instance.sent_date or disabled:
            self.fields["channel"].disabled = True
            self.fields["regions"].disabled = True
            self.fields["mode"].disabled = True

        self.fields["scheduled_send_date_day"].widget.attrs["min"] = str(
            timezone.now().date()
        )

        # Set the day and time fields
        if self.instance.scheduled_send_date:
            local_time = self.instance.scheduled_send_date_local
            self.fields["scheduled_send_date_day"].initial = local_time.date()
            self.fields["scheduled_send_date_time"].initial = local_time.time()
            self.fields["schedule_send"].initial = True

        if regions is None:
            regions = []
        if selected_regions is None:
            selected_regions = []

        self.fields["regions"].choices = [(obj.id, str(obj)) for obj in regions]
        self.fields["regions"].initial = selected_regions
        self.fields["is_template"].initial = template

    def clean(self):
        """
        Validate form fields which depend on each other, see :meth:`django.forms.Form.clean`

        :return: The cleaned form data
        :rtype: dict
        """
        cleaned_data = super().clean()

        if cleaned_data.get("schedule_send") and not cleaned_data.get(
            "scheduled_send_date_day"
        ):
            self.add_error(
                "scheduled_send_date_day",
                forms.ValidationError(
                    _("Cannot be unspecified"),
                ),
            )

        # Check if a template name is set when the message should be used as a template
        if cleaned_data.get("is_template") and not cleaned_data.get("template_name"):
            self.add_error(
                "template_name",
                forms.ValidationError(_("Please provide a name for your template")),
            )

        # Combine the scheduled send day and time into one timezone aware field
        if not self.errors and cleaned_data.get("schedule_send"):
            tzinfo = zoneinfo.ZoneInfo(str(timezone.get_current_timezone()))
            time = cleaned_data["scheduled_send_date_time"] or datetime.time()

            cleaned_data["scheduled_send_date"] = datetime.datetime.combine(
                cleaned_data["scheduled_send_date_day"], time
            ).replace(tzinfo=tzinfo)

            if cleaned_data["scheduled_send_date"] < timezone.now():
                self.add_error(
                    None,
                    forms.ValidationError(
                        _("The scheduled send date cannot be in the past"),
                    ),
                )

            if (
                cleaned_data["scheduled_send_date"].minute
                % settings.FCM_SCHEDULE_INTERVAL_MINUTES
            ):
                self.add_error(
                    "scheduled_send_date_time",
                    forms.ValidationError(
                        _("Can only schedule every %(interval)s minutes"),
                        params={"interval": settings.FCM_SCHEDULE_INTERVAL_MINUTES},
                    ),
                )

        return cleaned_data

    class Meta:
        model = PushNotification
        fields = [
            "channel",
            "regions",
            "mode",
            "scheduled_send_date",
            "is_template",
            "template_name",
        ]
        widgets = {
            "regions": CheckboxSelectMultiple(),
        }
