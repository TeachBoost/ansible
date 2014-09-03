% include(_template_dir + 'header.tpl')
    <form action="{{_basepath}}/email/?key={{key}}" method="POST">
        <label for="Sender">From</label>
        <input name="Sender" />
        <br />
        <label for="Subject">Subject</label>
        <input name="Subject" />
        <br />
        <label for="stripped-text">Body</label>
        <textarea cols="80" rows="20" name="stripped-text"></textarea>
        <br />
        <button type="submit">Send "email"</button>
    </form>
% include(_template_dir + 'footer.tpl')
