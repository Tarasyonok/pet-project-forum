import datetime
import django.utils.deconstruct
import django.utils.timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


@django.utils.deconstruct.deconstructible
class YearRangeValidator:
    def __init__(self, min_year, years_offset_from_current=0):
        self.min_year = min_year
        self.years_offset = years_offset_from_current

    def __call__(self, value):
        current_year = django.utils.timezone.now().year
        max_year = current_year + self.years_offset
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.year

        if not (self.min_year <= value <= max_year):
            raise ValidationError(
                self.get_error_message(current_year),
                params={"value": value},
            )

    def get_error_message(self, current_year):
        if self.years_offset > 0:
            return _("Year must be between %(min_year)s and %(max_year)s.") % {
                'min_year': self.min_year,
                'max_year': current_year + self.years_offset
            }
        elif self.years_offset < 0:
            return _("Year must be between %(min_year)s and %(max_year)s.") % {
                'min_year': self.min_year,
                'max_year': current_year + self.years_offset
            }

        return _("Year must be exactly %(current_year)s.") % {'current_year': current_year}