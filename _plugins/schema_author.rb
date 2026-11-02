# Normalize author identity only inside Schema.org JSON-LD.
require "json"

Jekyll::Hooks.register [:pages, :documents], :post_render do |page|
  next unless page.output_ext == ".html"

  page.output = page.output.gsub(/(<script\b[^>]*type=["']application\/ld\+json["'][^>]*>)(.*?)(<\/script>)/m) do
    opening, body, closing = Regexp.last_match.captures
    data = JSON.parse(body)
    changed = false
    normalize = lambda do |value|
      case value
      when Hash
        if value["@type"] == "Person" &&
            (value["@id"].to_s.match?(/#(?:author|publisher)\z/) ||
             ["dieghernan", "Diego Hernangómez"].include?(value["name"]))
          unless value["url"] == "https://dieghernan.github.io/"
            value["url"] = "https://dieghernan.github.io/"
            changed = true
          end
        end
        value.each_value { |child| normalize.call(child) }
      when Array
        value.each { |child| normalize.call(child) }
      end
    end
    normalize.call(data)
    opening + (changed ? "\n#{JSON.pretty_generate(data)}\n" : body) + closing
  end
end
