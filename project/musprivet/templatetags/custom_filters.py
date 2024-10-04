from django import template

register = template.Library()

@register.filter
def split_paragraphs(value):
    # Разделяем текст по строкам
    lines = value.split('\n')

    # Инициализируем список для хранения абзацев
    paragraphs = []

    # Инициализируем временный список для текущего абзаца
    current_paragraph = []

    for line in lines:
        # Если строка пустая, это конец текущего абзаца
        if line.strip() == '':
            if current_paragraph:
                paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []
        else:
            current_paragraph.append(line)

    # Добавляем последний абзац, если он есть
    if current_paragraph:
        paragraphs.append('\n'.join(current_paragraph))

    return paragraphs

@register.filter
def split_lines(value):
    return value.splitlines()
