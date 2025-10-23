from django import template

register = template.Library()

UNCENSORED_WORDS = {
   'европейск': 'e********',
   'ставк': 'c****',
   'человек': 'ч******'
}
# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value: str):
   for old, new in UNCENSORED_WORDS.items():
      value = value.replace(old, new)
   return value

@register.filter()
def format_time(value):
   format_string = '%d %b %Y'
   return value.strftime(format_string)

