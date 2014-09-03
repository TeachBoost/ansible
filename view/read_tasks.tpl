% include(_template_dir + 'header.tpl')
<h2>Tasks for week of {{start.strftime("%B %d, %Y")}}</h2>
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Task</th>
            <th>Date</th>
        </tr>
    </thead>
    <tbody>
        % for task in tasks:
            <tr>
                <td>{{task.user.name}}</td>
                <td>{{task.description}}</td>
                <td>{{task.date}}</td>
            </tr>
        % end
    </tbody>
</table>
<h2>
    <a href="{{_basepath}}/admin/tasks?w={{week+1}}">previous</a>
    <a href="{{_basepath}}/admin/tasks">current</a>
    <a href="{{_basepath}}/admin/tasks?w={{week-1}}">next</a>
    % end
</h2>
% include(_template_dir + 'footer.tpl')
