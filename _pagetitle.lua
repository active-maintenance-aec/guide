-- Markdown pages carry their title as a level-1 heading rather than YAML front
-- matter, so that GitHub renders them cleanly. Promote that heading to the
-- document title, so the browser tab and the title block use it.
function Pandoc(doc)
  if doc.meta.title ~= nil then
    return doc
  end
  for i, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 1 then
      doc.meta.title = block.content
      doc.meta.pagetitle = pandoc.utils.stringify(block.content)
      doc.blocks:remove(i)
      break
    end
  end
  return doc
end
