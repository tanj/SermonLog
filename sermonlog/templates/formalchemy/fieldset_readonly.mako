# -*- coding: utf-8 -*-
<tbody>
%for field in fieldset.render_fields.values():
%if field.requires_label:
  <tr>
    <td class="field_readonly">${field.label()|h}:</td>
    <td>${field.render_readonly()|n}</td>
  </tr>
%endif
%endfor
</tbody>
