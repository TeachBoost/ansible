% include(_template_dir + 'header.tpl')
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
    <h3><a href="{{_basepath}}/admin">Back to admin</a></h3>
% include(_template_dir + 'footer.tpl')
