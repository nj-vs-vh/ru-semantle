from backend.dependencies import get_pymorph_model


ma = get_pymorph_model()


print(ma.parse("печь"))
