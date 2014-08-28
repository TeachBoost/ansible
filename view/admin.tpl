% include(_template_dir + 'header.tpl')

<h1>Ansible Admin</h1>
<h3>User list</h3>
<form method="POST" action="{{_basepath}}/admin/delete">
    <table>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Admin</th>
            <th>Delete</th>
        </tr>
        % for user in users:
        <tr>
            <td><a href="{{_basepath}}/admin/{{user.id}}">{{user.name}}</a></td>
            <td>{{user.email}}</td>
            <td>{{"Yes" if user.is_admin else "No"}}
            <td><input name="{{user.id}}" type="checkbox" /></td>
        </tr>
        % end
    </table>
    <button type="submit">Delete Selected</button>
</form>
<h3>Create new user</h3>
<form method="POST" action="{{_basepath}}/admin/create">
    <label for="name">Name: </label>
    <input name="name" />
    <label for="email">Email: </label>
    <input name="email" type="email" />
    <button type="submit">Create</button>
</form>
<h3>
    <a href="{{_basepath}}/admin/tasks">View Tasks</a>
    % if email_url:
        <a href="{{email_url}}">Test email</a>
    % end
</h3>
% include(_template_dir + 'footer.tpl')
