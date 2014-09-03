% include(_template_dir + 'header.tpl')
<fieldset id="subscriptions">
    <legend>Manage my subscriptions</legend>
    <form method="post" action="{{_basepath}}/update/{{user.id}}">
        <ul class="cf"><!--
            % for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                --><li>
                    <div class="subscription-day">{{day}}</div>
                    <div class="subscription-time">
                        <input name="{{day}}" value="{{getattr(user, day) if getattr(user, day) else ''}}" />
                    </div>
                </li><!--
            % end
        --></ul>
        <button type="submit">Save</button>
    </form>
</fieldset>
% include(_template_dir + 'footer.tpl')
