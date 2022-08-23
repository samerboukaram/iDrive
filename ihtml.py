def Header():
    Header = """
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    """
    return Header


def Button(ID):
    html = """
    <script type=text/javascript>
    $(function() {$('a#""" + ID + """').on('click', function(e) {e.preventDefault(),$.getJSON('/""" + ID + """', function(data) {'//do nothing'});return false;});})
    </script>
    
    <a href=# id=""" + ID + """><button class="btn btn-default">""" + ID + """</button></a>
    """
    return html


def VideoStream():
    html = """
    <div class="container">
    <img src="{{ url_for('Video') }}" width="640" height="480">
    <div>
    """
    return html

Body = Header() + VideoStream() + Button("Forward") + Button("Backward") + Button("Stop") + Button("Left") + Button("Right")
print(Body)