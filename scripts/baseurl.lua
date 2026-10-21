-- Turn site-absolute links ("/research/") into links relative to the page
-- ("../research/"), so the Markdown can be written once and one build works on
-- any host. baseurl is the path from the page back to the root (".", "..", ...).
local baseurl = "."

local function fix(url)
  if url:sub(1, 1) == "/" and url:sub(2, 2) ~= "/" then
    return baseurl .. url
  end
  return url
end

return {
  { Meta = function(m)
      if m.baseurl then baseurl = pandoc.utils.stringify(m.baseurl) end
    end },
  { Link = function(el) el.target = fix(el.target); return el end,
    Image = function(el) el.src = fix(el.src); return el end,
    RawInline = function(el)
      if el.format == "html" then
        el.text = el.text:gsub('(href=")(/[^"]*)', function(a, u) return a .. fix(u) end)
                         :gsub('(src=")(/[^"]*)', function(a, u) return a .. fix(u) end)
      end
      return el
    end,
    RawBlock = function(el)
      if el.format == "html" then
        el.text = el.text:gsub('(href=")(/[^"]*)', function(a, u) return a .. fix(u) end)
                         :gsub('(src=")(/[^"]*)', function(a, u) return a .. fix(u) end)
      end
      return el
    end },
}
