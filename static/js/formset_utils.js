/*
    Script for cloning and removing forms in a formset.
    Based on the following scripts:
    - https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
    - https://webdevdesigner.com/q/dynamically-adding-a-form-to-a-django-formset-with-ajax-14260/
*/

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();

    // Update name and id of each input which is not a button
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        if ($(this).attr('type') == 'hidden') {
            // If input type is "hidden", we'll assume we need to keep the value
            $(this).attr({'name': name, 'id': id}).removeAttr('checked');
            if ($(this).attr('id').endsWith('-id')) {
                $(this).attr('value', '');
            }
        }
        else {
            // If input type is different than "hidden", we'll systematically erase the value
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });

    // Update each copied label
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });

    // Update the total number of forms in the formset
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.formset-row').remove();
        var forms = $('.formset-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}