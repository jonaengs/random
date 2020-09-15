using DelimitedFiles

function pprint(M)
    for i = 1:size(M, 1)
        println(M[i, :])
    end
end

function clampr(range, _max, _min=1)
    return max(_min, first(range)) : min(_max, last(range))
end


function standard_compute(current, repeat=0)
    next::Array{Int8, 2} = Array{Int8, 2}(undef, m, n)
    for j = 1:n, i = 1:m  # column major, se we iterate over rows inside
        num_neighbors::Int8 = 0
        for y = clampr(j-1:j+1, n), x = clampr(i-1:i+1, m)  # same
            if !(x==i && y==j)
                num_neighbors += current[x, y]
            end
        end
        next[i, j] = num_neighbors == 3 || (num_neighbors == 2 && current[i, j] == 1)
    end

    if repeat > 0
        return standard_compute(next, repeat-1)
    end
    return next
end

function my_compute(current, repeat=0)
    function calc_cols!(M, out)
        out[:, 1] += M[:, 2]
        out[:, 2:n-1] = M[:, 1:n-2] + M[:, 3:n]
        out[:, n] += M[:, n-1]
    end
    """
    for i = 2:m-1
        out[i, :] += M[i-1, :] + M[i+1, :]
    end
    """
    function calc_rows!(M, out)
        out[1, :] += M[2, :]
        out[2:m-1, :] = M[1:m-2, :] + M[3:m, :]
        out[m, :] += M[m-1, :]
    end
    function set_live_dead!(M)
        for j = 1:n, i = 1:m
            M[i, j] = M[i, j] == 3 || (M[i, j] == 2 && current[i, j] == 1)
        end
    end

    next::Array{Int8, 2} = zeros(Int8, m, n)

    calc_rows!(current, next)
    calc_cols!(next[:, :], next)
    calc_cols!(current, next)

    set_live_dead!(next)

    if repeat > 0
        return my_compute(next, repeat-1)
    end
    return next
end

m, n = 1000, 10000
r = 5
function call_stuff()
    current1::Array{Int8, 2} = rand(m, n) .> 0.5
    current2 = current1[:, :] 
    # @time std_next = standard_compute(current2, r)
    @time my_next = my_compute(current1, r)
end

call_stuff()
