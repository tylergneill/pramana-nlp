<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="div/p[@ll_n=1]">

{<xsl:value-of select="@ll"/>}

[<xsl:value-of select="@pb"/>.<xsl:value-of select="@p_n"/>]

<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="div/p[not(@ll_n=1)]">

[<xsl:value-of select="@pb"/>.<xsl:value-of select="@p_n"/>]

<xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>