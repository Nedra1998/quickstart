function! s:SetGlobalOption(opt, val)
  if !exists("g:" . a:opt)
    let g:{a:opt} = a:val
  endif
endfunction
