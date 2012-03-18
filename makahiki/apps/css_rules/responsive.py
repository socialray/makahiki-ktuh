"""Provides variables (strings and dicts) that implement mappings of ids to CSS classes.

Templates that use class_tags and insert_classes refer to this module. Note that some of the "ids"
are more like class names.  These rules act like "macro expansions" in the templates. If True, the
classes will be inserted.  Otherwise, the tags will be empty strings.

Makahiki 2 note: CSS information specific to particular widgets should be encapsulated with that
widget.
"""

RETURN_CLASSES = True

CSS_IMPORTS = """
<link href="{0}css/bootstrap.css" rel="stylesheet">
<link href="{0}css/bootstrap-responsive.css" rel="stylesheet">
<link href="{0}css/bootstrap-override.css" rel="stylesheet">
<link href="{0}css/makahiki-structure.css" rel="stylesheet">
<!-- link href="css/<page>.css" rel="stylesheet" -->
<link rel="stylesheet/less" type="text/css" href="{0}css/theme.less">
<script src="{0}js/less-1.3.0.min.js" type="text/javascript"></script>
"""