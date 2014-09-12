% include(_template_dir + 'header.tpl')
    <fieldset id="user-settings">
    <legend>Settings for {{person.name}}</legend>
    <form method="post">
        <ul class="cf subscriptions"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <select name="{{day}}">
                        % has = getattr(person, day) is not None
                        <option> None </option>
                        % for hour in range(0, 24):
                            <option value="{{hour}}" {{'selected' if has and int(getattr(person, day) + person.timezone) == hour else ''}}>
                                {{hour % 12 or 12}}:00 {{'A' if hour < 12 else 'P'}}M
                            </option>
                        % end
                    </select>
                    </div>
                </li><!--
            % end
        --></ul>
        <div class="user-details">
            <div>
                <label for="serial">Serial: </label>
                <input class="serial" name="serial" value="{{person.serial}}" />
                <label for="email">Email: </label>
                <input class="email" name="email" value="{{person.email}}" />
                <label>
                    <input type="checkbox" name="send_reminders" {{'checked' if person.send_reminders else ''}}>
                    Send Reminders
                </label>
            </div>
            <div>
                <label>Timezone: </label>
                <select name="timezone">
                    % for timezone in timezones:
                        <option value="{{timezone[0]}}" {{'selected' if timezone[0] == person.timezone else ''}}>
                            {{timezone[1]}}
                        </option>
                    % end
                </select>
            </div>
            <div>
                <label>
                    <input type="checkbox" name="is_admin" {{'checked' if person.is_admin else ''}}>
                    Admin
                </label>
                <button type="submit">Save</button>
            </div>
        </div>
    </form>
    </fieldset>
% include(_template_dir + 'footer.tpl')
