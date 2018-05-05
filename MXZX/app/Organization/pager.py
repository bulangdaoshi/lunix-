from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def __init__(self,current_page,per_pager_nums,*args,**kwargs):
        self.current_page=int(current_page)
        self.per_pager_nums=int(per_pager_nums)
        super(CustomPaginator,self).__init__(*args,**kwargs)

    def page_nums_range(self):
        if self.per_pager_nums>=self.num_pages:
            return range(1,self.num_pages+1)
        part = int(self.per_pager_nums/2)
        if self.current_page<=part:
            return range(1,self.per_pager_nums+1)

        if (self.current_page+part)>self.num_pages:
            return range(self.num_pages-self.per_pager_nums+1,self.num_pages+1)

        return range(self.current_page-part,self.current_page+part+1)