% include(_template_dir + 'header.tpl')
<fieldset id="user-settings">
    <legend>Manage subscriptions for {{user.name}}</legend>
    <form method="post" action="{{_basepath}}/update/{{user.id}}">
        <ul class="cf subscriptions"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <select name="{{day}}">
                        % has = getattr(user, day) is not None
                        <option> None </option>
                        % for hour in range(0, 24):
                            <option value="{{hour}}" {{'selected' if has and int(getattr(user, day) + user.timezone) == hour else ''}}>
                                {{hour % 12 or 12}}:00 {{'A' if hour < 12 else 'P'}}M
                            </option>
                        % end
                    </select>
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
<h2><a href="{{_basepath}}/tasks/{{user.id}}">View my tasks</a></h2>
% include(_template_dir + 'footer.tpl')
