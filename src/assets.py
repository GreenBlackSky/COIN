from flask_assets import Bundle


def pack_js(assets):
    js_bundle = Bundle('src/js/script.js', filters='jsmin', output='dst/js/script.min.js')
    assets.register('js_assets', js_bundle)
    js_bundle.build()