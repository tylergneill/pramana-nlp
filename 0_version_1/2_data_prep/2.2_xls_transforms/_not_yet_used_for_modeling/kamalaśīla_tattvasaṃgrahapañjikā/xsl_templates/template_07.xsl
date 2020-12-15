<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="p[@type]">

[<xsl:value-of select="@locus"/>]

<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="p[not(@type)]">

[<xsl:value-of select="@locus"/>]

<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="head">

{<xsl:value-of select="parent::div/@n"/>_<xsl:value-of select="."/>}

</xsl:template>

<xsl:template match="trailer">

〈<xsl:value-of select="."/>〉

</xsl:template>

<!-- 
lb
 -->

</xsl:stylesheet>