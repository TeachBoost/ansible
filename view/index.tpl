% include(_template_dir + 'header.tpl')
<fieldset id="user-settings">
    <legend>Manage subscriptions for {{user.name}}</legend>
    <form method="post" action="{{_basepath}}/update/{{user.id}}">
        <ul class="cf subscriptions"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <div class="subscription-time">
                        <input name="{{day}}" value="{{int(getattr(user, day) + user.timezone) if getattr(user, day) else ''}}" />
                    </div>
                </li><!--
            % end
        --></ul>
        <div class="user-details">
            <div>
                <label>Timezone: </label>
                <select name="timezone">
                    % for timezone in timezones:
                        <option value="{{timezone[0]}}" {{'selected' if timezone[0] == user.timezone else ''}}>
                            {{timezone[1]}}
                        </option>
                    % end
                </select>
            </div>
            <div>
                <label>
                    <input type="checkbox" name="send_reminders" {{'checked' if user.send_reminders else ''}}>
                    Send Update Reminders
                </label>
            </div>
        <button type="submit">Save</button>
    </form>
</fieldset>
% include(_template_dir + 'footer.tpl')
