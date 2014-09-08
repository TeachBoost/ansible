% include(_template_dir + 'header.tpl')
<fieldset id="user-settings">
    <legend>Manage subscriptions for {{user.name}}</legend>
    <form method="post" action="{{_basepath}}/update/{{user.id}}">
        <ul class="cf subscriptions"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <div class="subscription-time">
                        <input name="{{day}}" value="{{getattr(user, day) if getattr(user, day) else ''}}" />
                    </div>
                </li><!--
            % end
        --></ul>
        <label>
            <input type="checkbox" name="send_reminders" {{'checked' if user.send_reminders else ''}}>
            Send Update Reminders
        </label>
        <button type="submit">Save</button>
    </form>
</fieldset>
% include(_template_dir + 'footer.tpl')
