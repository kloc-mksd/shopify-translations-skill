"""Decide whether a translatable-content value is human-readable text worth translating."""
import re

SKIP_KEY_PATTERNS = [
    r'(^|[._])image($|[._\d])', r'(^|[._])icon($|[._\d])', r'(^|[._])logo($|[._\d])',
    r'_image(_\d+)?$', r'(^|[._])url($|[._])', r'_url$', r'(^|[._])video',
    r'(^|[._])color', r'_scheme$', r'font_family', r'aspect_ratio', r'(^|[._])svg',
    r'_id$', r'(^|[._])link$', r'_link$', r'_handle$', r'(^|[._])icon_', r'_media$',
    r'(^|[._])media_set$', r'_gid$', r'^gid', r'_class$', r'_css$', r'padding', r'margin',
    r'_size$', r'_width$', r'_height$', r'_align', r'_position', r'_ratio$', r'_speed$',
    r'_delay$', r'_count$', r'_limit$', r'_columns?$', r'_rows?$',
]
SKIP_KEY_RE = re.compile('|'.join(SKIP_KEY_PATTERNS), re.I)

URL_RE = re.compile(r'^\s*(https?://|shopify://|//|/[a-z0-9\-_/]*$|mailto:|tel:)', re.I)
FILE_RE = re.compile(r'^\s*\S+\.(jpe?g|png|svg|webp|gif|mp4|webm|pdf|css|js|json|woff2?)\s*$', re.I)
NUMERICISH_RE = re.compile(r'^\s*[\d\s.,:/%+\-x×]*\s*$')
HEX_RE = re.compile(r'^\s*#?[0-9a-f]{3,8}\s*$', re.I)
GID_RE = re.compile(r'^\s*gid://', re.I)
HANDLE_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)+$')          # slug-looking, no spaces
BOOL_RE = re.compile(r'^\s*(true|false|yes|no|on|off)\s*$', re.I)

# keys that are legitimate text even though a pattern above might catch them
KEEP_KEYS = {'meta_title', 'meta_description', 'title', 'body_html', 'summary_html',
             'description', 'label', 'name', 'value', 'body'}

# leaf suffixes that always denote copy, even when the key also contains e.g. "image"
KEEP_SUFFIX_RE = re.compile(
    r'(_|^)(label|text|heading|subheading|subtext|subtitle|title|caption|description|'
    r'content|cta|button|placeholder|message|note|tagline|alt|copy|blurb|answer|'
    r'question|summary|name)(_\d+)?$', re.I)

TRANSLATE_HANDLES = False

# --- things the storefront COMPARES or parses; translating them breaks the theme ---
# leaf keys that hold machine values (tags, filter params, css keywords, tokens)
MACHINE_LEAF_RE = re.compile(
    r'(^|_)(param|params|tag|tags|slug|key|code|token|enum|mode|layout|style|styles|'
    r'variant|preset|ratio|format|number)$|^tag_|_param$|_tag$', re.I)
# keys some themes string-compare against a Liquid value (e.g. iwasasari:
# sections/main-collection-product-grid-all-clothing.liquid: filter.label == settings.size_filter_label)
FROZEN_KEYS = {'size_filter_label', 'size_filter_param'}
CSS_KEYWORDS = {'none', 'auto', 'inherit', 'initial', 'unset', 'solid', 'dashed', 'dotted',
                'hidden', 'transparent', 'normal', 'bold', 'italic', 'center', 'left', 'right',
                'top', 'bottom', 'cover', 'contain', 'block', 'inline', 'flex', 'grid'}
EMAIL_RE = re.compile(r'^\s*[^@\s]+@[^@\s]+\.[a-z]{2,}\s*$', re.I)
TOKEN_RE = re.compile(r'^\s*[\[\{][a-z0-9_\-.]+[\]\}]\s*$', re.I)
EMPTY_HTML_RE = re.compile(r'^\s*(<[^>]+>|\s|&nbsp;)*\s*$')


def is_translatable(key, value, ctype=None):
    """Return (bool, reason)."""
    if value is None:
        return False, 'null'
    v = value.strip()
    if not v:
        return False, 'empty'
    kbase = key.split(':')[0]           # theme keys carry a :digestish suffix
    leaf = kbase.split('.')[-1]

    if leaf == 'handle' or kbase.endswith('.handle') or kbase == 'handle':
        if not TRANSLATE_HANDLES:
            return False, 'handle'
    if leaf in FROZEN_KEYS:
        return False, 'frozen-compared-in-liquid'
    # …unless the leaf is plainly a copy field (tag_label, tag_heading, style_text…)
    if MACHINE_LEAF_RE.search(leaf) and not KEEP_SUFFIX_RE.search(leaf):
        return False, 'machine-value'
    if EMPTY_HTML_RE.match(v):
        return False, 'empty-html'
    if EMAIL_RE.match(v):
        return False, 'email'
    if TOKEN_RE.match(v):
        return False, 'token'
    if v.strip().lower() in CSS_KEYWORDS:
        return False, 'css-keyword'
    if GID_RE.match(v):
        return False, 'gid'
    if URL_RE.match(v):
        return False, 'url'
    if FILE_RE.match(v):
        return False, 'filename'
    if HEX_RE.match(v) and len(v) <= 9:
        return False, 'color'
    if BOOL_RE.match(v):
        return False, 'boolean'
    if NUMERICISH_RE.match(v):
        return False, 'numeric'
    if ctype in ('LINK', 'FILE_REFERENCE', 'IMAGE_REFERENCE', 'COLOR', 'URI'):
        if leaf not in KEEP_KEYS:
            return False, f'type:{ctype}'
    if leaf not in KEEP_KEYS and not KEEP_SUFFIX_RE.search(leaf) and SKIP_KEY_RE.search(kbase):
        return False, 'key-pattern'
    # slug-looking single token with no spaces and no capitals -> likely a handle/value ref
    if ' ' not in v and HANDLE_RE.match(v) and leaf not in KEEP_KEYS and not KEEP_SUFFIX_RE.search(leaf):
        return False, 'sluglike'
    # single non-letter char
    if len(v) < 2 and not v.isalpha():
        return False, 'too-short'
    if not re.search(r'[A-Za-z]', v):
        return False, 'no-letters'
    return True, 'ok'
