/**
 * Created by Administrator on 2018/3/28.
 */
//��ǰʱ��
function getDate(){
            var curDate = new Date();
            var year =curDate.getFullYear();
            var month = curDate.getMonth() + 1;
            var day = curDate.getDate();
            return year + '-' + 'month' + '-' + day;
}