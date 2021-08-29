import datetime
import time

from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone

from .models import CustomUser, SearchHistory


def date_convert_to_str(date_str=None):
    if date_str is not None:
        try:
            a = date_str.split("/")
            date_str = str(a[2] + "-" + a[0] + "-" + a[1])
            date_str = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return date_str
        except IndexError:
            return None
    return None


def email_check(email):
    mailExist = []
    mailExist = CustomUser.objects.filter(email=email)
    if len(mailExist) > 0:
        return True
    return False


def search_history_info_saved(search, user=None):
    # print("---------search", search)
    a = SearchHistory.objects.filter(search_keyword__exact=search).distinct().count()
    if a >= 1:
        if user is not None:
            if SearchHistory.objects.filter(search_keyword__exact=search, user=user).distinct().exists():
                SearchHistory.objects.filter(search_keyword__exact=search, user=user).update(
                    updated_at=timezone.now(),
                    keyword_count=F('keyword_count') + 1,
                    keyword_count_by_user=F('keyword_count_by_user') + 1)
                pass
            else:
                a = SearchHistory.objects.get(search_keyword=search)
                a.keyword_count = a.keyword_count + 1
                a.updated_at = timezone.now(),
                a.keyword_count_by_user = a.keyword_count_by_user + 1
                a.user.add(user)
                a.save()
        else:
            SearchHistory.objects.filter(search_keyword__exact=search).update(
                updated_at=timezone.now(),
                keyword_count=F('keyword_count') + 1)

    else:
        if user is not None:
            search_created = SearchHistory.objects.create(search_keyword=search)
            search_created.user.add(user)
            search_created.save()

        else:
            search_created = SearchHistory.objects.create(search_keyword=search)
            search_created.save()
