from django.views.generic import TemplateView

from ...utils.linkcheck_utils import get_url_count


class AnalyticsView(TemplateView):
    """
    View to show all not-working links in the content.
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "analytics/analytics_overview.html"

    def get_context_data(self, **kwargs):
        r"""
        Extend context by amount of links per link filter

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The context dictionary
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        count_dict = get_url_count(kwargs.get("region_slug"))
        context.update(count_dict)
        context["current_menu_item"] = "analytics"
        return context
