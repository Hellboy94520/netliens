from .language import LanguageModel, LanguageAvailable

def get_all_model_in_order(model, **kwargs):
    model_list = []
    for _model in model.objects.filter(parent=None, **kwargs).order_by('order'):
        model_list.append(_model)
        model_list.extend(_model.get_children_list(**kwargs))
    return  { _model.pk : _model for _model in model_list }

def get_all_modelWithData_in_order(model, language: LanguageAvailable = LanguageAvailable.EN.value, **kwargs):
    model_map = get_all_model_in_order(model=model, **kwargs)
    modelWithData_map = dict()
    for _pk, _model in model_map.items():
        modelWithData_map[_model] = _model.get_data(language=language)
    return modelWithData_map

def get_all_modelDataWithPosition_in_order(model, language: LanguageAvailable = LanguageAvailable.EN.value, **kwargs):
    model_map = get_all_model_in_order(model=model, **kwargs)
    modelWithData_map = dict()
    for _pk, _model in model_map.items():
        parent_quantity = 0
        parent = _model.parent
        while parent:
            parent_quantity += 1
            parent = parent.parent
        modelWithData_map[_model] = [_model.get_data(language=language), parent_quantity]
    return modelWithData_map
