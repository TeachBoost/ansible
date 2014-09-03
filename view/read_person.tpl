% include(_template_dir + 'header.tpl')
    <fieldset id="subscriptions">
    <legend>Settings for {{person.name}}</legend>
    <form method="post">
        <ul class="cf"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <div class="subscription-time">
                        <input name="{{day}}" value="{{getattr(person, day) if getattr(person, day) else ''}}" />
                    </div>
                </li><!--
            % end
        --></ul>
        <button type="submit">Save</button>
        <div class="admin-toggle">
            <label>
                <input type="checkbox" name="is_admin" {{'checked' if person.is_admin else ''}}>
                Admin
            </label>
        </div>
    </form>
    </fieldset>
    
    
    <!--
    <h1>Settings for {{person.name}}</h1>
    <form method="post">
        <table>
            <tr>
                <th>Day</th>
                <th>Time</th>
            </tr>
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                <tr>
                    <td>{{day}}</td>
                    <td><input style="width:40px" name="{{day}}" value="{{getattr(person, day) if getattr(person,day) else ''}}" /></td>
                </tr>
            % end
        </table>
            <div>
                <label>
                    Admin
                    <input type="checkbox" name="is_admin" {{'checked' if person.is_admin else ''}}>
                </label>
            </div>
        <button type="submit">Save</button>
    </form>
    -->
% include(_template_dir + 'footer.tpl')
