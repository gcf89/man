
# Ф-я для добавления значения в файлы ini
# Проверяется наличие параметра в указанном блоке

f_set_config_value()
{
    local conf
    local block
    local param
    local value

    block="$1"
    param="$2"
    value="$3"
    conf="$CFG_USER_SIDE_INI_CONFIG"

    local block_start
    block_start=0
    if ! grep -q -F "[$block]" $conf; then
        # insert block at the end 
        echo "[$block]" >> $conf
    else
        block_start=$(grep -n -F "[$block]" $conf | tail -n1 | cut -d: -f1)
    fi

    if [[ $block_start -eq 0 ]]; then
        # insert param=value at the end
        echo "${param}=${value}" >> $conf
    else
        # get end of block: EOF, next block
        block_end=$(awk -v bs=$block_start '{ if (NR > bs && $0 ~ /^\[/) {print NR} } END {print NR}' $conf | head -n1)

        if sed -n "$block_start,$block_end p" $conf  | grep -q -E "$param=.*"; then
            # replace
            sed -i -e "${block_start},${block_end}s/${param}=.*/${param}=${value}/" $conf
        else
            # insert
            #sed -i "$((block_start + 1)) i ${param}=${value}" $conf
            sed -i "${block_start},${block_end}s/\[$block\]/\[$block\]\n${param}=${value}/" $conf
        fi
    fi
}
