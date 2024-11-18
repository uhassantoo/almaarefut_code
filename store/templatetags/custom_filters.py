from django import template

register = template.Library()

@register.filter
def group_attributes(attributes):
    attribute_dict = {}
    result = []

    for attribute in attributes:
        if attribute.specification.name in attribute_dict:
            a_v = f'<label class="btn rounded-pill basket"> <input type="radio" name="{attribute.specification.name}" value="{attribute.id}">{attribute.value}</label>'
            attribute_dict[attribute.specification.name].append(a_v)
        else:
            a_v = f'<label class="btn rounded-pill basket"> <input type="radio" name="{attribute.specification.name}" value="{attribute.id}" checked>{attribute.value}</label>'
            attribute_dict[attribute.specification.name] = [a_v]

    for key, values in attribute_dict.items():
        result.append(f'{key} <br /> <div class="d-flex gap-2">{" ".join(values)}</div>')

    return '<br/> <br/>'.join(result)
