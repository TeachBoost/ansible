<div>
    <h2>
        % if defined('user') and user.is_admin:
            <a href="{{_basepath}}/admin">Ansible Admin</a>
        % elif not defined('hide_link') or not hide_link:
            <a href="{{_basepath}}">Ansible</a>
        % end
    </h2>
</div>
</main>

</body>
</html>
