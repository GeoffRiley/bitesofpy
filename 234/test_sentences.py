import pytest

from sentences import capitalize_sentences

lorem_ipsum = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor!
Pulvinar sapien et ligula ullamcorper malesuada proin libero nunc consequat?
Sed viverra tellus in hac habitasse platea dictumst vestibulum.
Morbi tempus iaculis urna id volutpat.
Enim blandit volutpat maecenas volutpat.
Morbi tristique senectus et netus!
Massa tincidunt nunc pulvinar sapien?
Nunc aliquet bibendum enim facilisis gravida neque convallis a.
Enim blandit volutpat maecenas volutpat blandit aliquam etiam erat velit.
Id diam maecenas ultricies mi eget mauris?
Diam quis enim lobortis scelerisque fermentum dui faucibus in ornare!
Gravida in fermentum et sollicitudin ac orci phasellus!
Ut diam quam nulla porttitor massa id neque aliquam.
Sit amet dictum sit amet justo donec enim diam vulputate.
Risus sed vulputate odio ut?
Justo eget magna fermentum iaculis eu non!
At auctor urna nunc id.
At erat pellentesque adipiscing commodo elit at imperdiet!
Molestie nunc non blandit massa enim nec dui?
Lorem donec massa sapien faucibus et molestie ac feugiat.
""".strip().splitlines()
text1, text2, text3 = lorem_ipsum[:5], lorem_ipsum[5:13], lorem_ipsum[13:]


@pytest.mark.parametrize("text", [
    text1, text2, text3
])
def test_capitalize_sentences(text):
    expected = " ".join(text)
    arg = expected.lower()
    assert capitalize_sentences(arg) == expected
