from bs4 import BeautifulSoup as bs

html_string = '''
<div class="bg-black border border-gray-700 rounded-none p-4 w-full lg:w-2/3 mx-auto" data-post_id="" data-type="text_post">
  <div class="flex items-center justify-between mb-2">
    <h1 class="text-white text-xl font-semibold" data-type="title">Text Post Title</h1>
    <span class="text-gray-400 text-sm" data-type="date">2024-06-10</span>
  </div>
  <p class="text-white" data-type="caption">Lorem ipsum...</p>
  <div class="flex justify-start flex-wrap" data-type="link_container">
    <a class="pr-3 text-yellow-400 hover:text-yellow-600 hover:underline transition-colors" data-type="link" href="https://lipsum.app/random/500x500">Link 1</a>
  </div>
</div>
'''

soup = bs(html_string, "html.parser")
tag = soup.find(attrs={"data-post_id": True})
tag["data-post_id"] = "000001"
print(tag)  # This will print the div as expected