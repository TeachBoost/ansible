% include(_template_dir + 'header.tpl')
<h1>Welcome to Ansible {{user.name}}</h1>
<div>
    <h3>Manage my subscriptions</h3>
    <form method="post" action="{{_basepath}}/update/{{user.id}}">
        <table>
            <tr>
                <th>Day</th>
                <th>Time</th>
            </tr>
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                <tr>
                    <td>{{day}}</td>
                    <td><input style="width:40px" name="{{day}}" value="{{getattr(user, day) if getattr(user, day) else ''}}" /></td>
                </tr>
            % end
        </table>
        <button type="submit">Save</button>
    </form>
</div>
% if user.is_admin:
    <div>
        <h3><a href="{{_basepath}}/admin">Ansible Admin</a></h3>
    </div>
% end
% include(_template_dir + 'footer.tpl')
