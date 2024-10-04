from musprivet.models import Tag, Name


def get_grouped_names(tag_slug):
    grouped_names = {}
    if getattr(Tag.objects.get(slug=tag_slug), 'is_male_name_related'):
        gender = 'M'
        names = Name.objects.filter(gender=gender)
        for name in names:
            first_letter = name.name[0].upper()
            if first_letter not in grouped_names:
                grouped_names[first_letter] = []
            grouped_names[first_letter].append(name)
        sorted_letters = sorted(grouped_names.keys())
        grouped_names_dict = {letter: grouped_names[letter] for letter in sorted_letters}
        return grouped_names_dict
    elif getattr(Tag.objects.get(slug=tag_slug), 'is_female_name_related'):
        gender = 'F'
        names = Name.objects.filter(gender=gender).order_by('name')
        for name in names:
            first_letter = name.name[0].upper()
            if first_letter not in grouped_names:
                grouped_names[first_letter] = []
            grouped_names[first_letter].append(name)
        sorted_letters = sorted(grouped_names.keys())
        grouped_names_dict = {letter: grouped_names[letter] for letter in sorted_letters}
        return grouped_names_dict