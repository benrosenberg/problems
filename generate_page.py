import os
import json

with open('problems.json', 'r') as f:
    problems = json.loads(f.read())

header = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <meta name="author" content="Ben Rosenberg" />
  <title>Problem set</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.11.1/katex.min.js"></script>
  <script>document.addEventListener("DOMContentLoaded", function () {
   var mathElements = document.getElementsByClassName("math");
   var macros = [];
   for (var i = 0; i < mathElements.length; i++) {
    var texText = mathElements[i].firstChild;
    if (mathElements[i].tagName == "SPAN") {
     katex.render(texText.data, mathElements[i], {
      displayMode: mathElements[i].classList.contains('display'),
      throwOnError: false,
      macros: macros,
      fleqn: false
     });
  }}});
  </script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.11.1/katex.min.css" />
  <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>
  <![endif]-->
  <style>
    body {
        font-family: sans-serif;
    }
    ul {
        list-style: none;
        list-style-position: inside;
        padding-left: 0;
    }
    li {
        padding-left: 10px;
    }
    img {
        position: relative;
    }
    .content {
        margin-left: auto;
        margin-right: auto;
        max-width: 800px;
    }
  </style>
</head>
<body>
<div class="content">
<h2>Problem set</h2>
<h3>by <a href="https://benrosenberg.info">Ben Rosenberg</a></h3>
<p>Problems are rated as follows:</p>
<div>
<table style="text-align: center; margin-left: auto; margin-right: auto;">
<tr><th>Difficulty</th><th>Meaning</th></tr>
<tr><td><img src="media/0.png"></td><td>Easy</td></tr>
<tr><td><img src="media/1.png"></td><td>Intermediate</td></tr>
<tr><td><img src="media/2.png"></td><td>Hard</td></tr>
<tr><td><img src="media/3.png"></td><td>Harder</td></tr>
<tr><td><img src="media/4.png"></td><td>Hardest</td></tr>
<tr><td><img src="media/5.png"></td><td>Dubious</td></tr>
<tr><td><img src="media/6.png"></td><td>Questionable</td></tr>
<tr><td><img src="media/7.png"></td><td>Stupid</td></tr>
</table>
<div>
<div>
<ul>
'''

footer = '''
</ul>
</div>
</div>
</body>
</html>
'''

print(len(problems['problems']), 'problems')

def katexify(text):
    print(text)
    with open('tmp.txt', 'w') as f:
        f.write(text)
    cmd = 'pandoc tmp.txt --katex -o tmp.html'
    os.system(cmd)
    with open('tmp.html', 'r') as f:
        output = f.read()
    return output

def render_problem(problem):
    number = problem['number']
    name = problem['name']
    difficulty = problem['difficulty']
    content = problem['contents']
    output = katexify(content).lstrip('<p>').rstrip('</p>')
    number_string = str(number) + '.'
    extensions = ''
    if problem['extensions']:
        extensions = '<ul>'
        for i,ext in enumerate(problem['extensions']):
            ext_difficulty = ext['difficulty']
            ext_output = katexify(ext['contents']).lstrip('<p>').rstrip('</p>')
            ext_number_string = '<li>' + str(number) + '.'  + str(i+1) + ' '
            ext_difficulty_image = '<img src="media/{}.png">'.format(ext_difficulty)
            extensions += ext_number_string + ext_difficulty_image + ' ' + ext_output + '</li>'
        extensions += '</ul>'
    difficulty_image = '<img src="media/{}.png">'.format(difficulty)
    middle = number_string + f' [{name}] ' + difficulty_image + ' ' + output + extensions
    item = '<li>' + middle + '</li>'
    return item

problem_html = ''

problems['problems'].sort(key=lambda x:x['number'])

for problem in problems['problems']:
    problem_html += render_problem(problem)

print(problem_html)

with open('index.html', 'w') as f:
    f.write(header + problem_html + footer)

os.remove('tmp.txt')
os.remove('tmp.html')