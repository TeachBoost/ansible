% include(_template_dir + 'header.tpl')
    <form action="{{_basepath}}/email/?key={{key}}" method="POST">
        <label for="Sender">From</label>
        <input name="Sender" />
        <label for="Subject">Subject</label>
        <input name="Subject" />
        <label for="stripped-text">Body</label>
        <textarea cols="80" rows="20" name="stripped-text"></textarea>
        <button type="submit">Send "email"</button>
    </form>
    <h3><a href="{{_basepath}}/admin">Back to admin</a></h3>
% include(_template_dir + 'footer.tpl')
